import { Component, ViewChild, ElementRef, OnDestroy } from "@angular/core";

import { interval, Subscription } from "rxjs";
import jsPDF from "jspdf";
import { UploadCallService } from "../../../services/upload-call.service";
import { MatCardModule } from "@angular/material/card";
import { MatButtonModule } from "@angular/material/button";
import { MatIconModule } from "@angular/material/icon";
import { MatProgressBarModule } from "@angular/material/progress-bar";
import { MatProgressSpinnerModule } from "@angular/material/progress-spinner";
import { MatDividerModule } from "@angular/material/divider";
import { MatListModule } from "@angular/material/list";
import {MatChip, MatChipsModule} from "@angular/material/chips";
import { CommonModule } from "@angular/common";

interface CallSummary {
  call_id: string;
  summary: string[];
  sentiment: string;
  category: string;
  action_items: string[];
  customer_requests: string[];
  resolution_status: string;
  priority: string;
  tags: string[];
  agent_performance: string;
  follow_up_required: boolean;
  processed_at: string;
}

interface TranscriptResult {
  call_id: string;
  transcript: string;
  audio_duration: number;
  processed_at: string;
}

@Component({
  selector: "app-upload-call",
  imports: [
    MatCardModule,
    MatButtonModule,
    MatIconModule,
    MatProgressBarModule,
    MatProgressSpinnerModule,
    MatListModule,
    MatDividerModule,
    MatChipsModule,
      MatChip,
    CommonModule,
  ],
  templateUrl: "./upload-call.component.html",
  styleUrls: ["./upload-call.component.scss"],
})
export class UploadCallComponent implements OnDestroy {
  @ViewChild("fileInput") fileInput!: ElementRef<HTMLInputElement>;

  selectedFile: File | null = null;
  isDropzoneActive = false;
  isUploading = false;
  isProcessing = false;
  processingStatus = "50% of the call has been transcribed.";
  callResult: CallSummary | null = null;
  transcriptResult: TranscriptResult | null = null;

  private pollingSub?: Subscription;
  private processingUrl: string = "";

  constructor(private uploadService: UploadCallService) {}

  onFileSelected(event: Event) {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length) {
      this.selectedFile = input.files[0];
    }
  }

  onFileDrop(event: DragEvent) {
    event.preventDefault();
    this.isDropzoneActive = false;
    if (event.dataTransfer && event.dataTransfer.files.length) {
      this.selectedFile = event.dataTransfer.files[0];
    }
  }

  onDragOver(event: DragEvent) {
    event.preventDefault();
    this.isDropzoneActive = true;
  }

  onDragLeave(event: DragEvent) {
    event.preventDefault();
    this.isDropzoneActive = false;
  }

  removeFile() {
    this.selectedFile = null;
    if (this.fileInput) {
      this.fileInput.nativeElement.value = "";
    }
  }

  uploadFile() {
    if (!this.selectedFile) return;
    this.isUploading = true;
    this.isProcessing = false;
    this.processingStatus = "";
    this.callResult = null;
    this.transcriptResult = null;

    this.uploadService.uploadCall(this.selectedFile).subscribe({
      next: (res) => {
        this.isUploading = false;
        this.isProcessing = true;
        this.processingStatus = res.message || "Processing audio...";
        this.processingUrl = res.processing_url;
        this.startPolling();
      },
      error: (err) => {
        this.isUploading = false;
        this.processingStatus = "Upload failed. Please try again.";
      },
    });
  }

  startPolling() {
    if (!this.processingUrl) return;
    this.pollingSub = interval(2000).subscribe(() => {
      this.uploadService.getProcessingStatus(this.processingUrl).subscribe({
        next: (res) => {
          if (res.status && res.status !== "completed") {
            this.processingStatus = res.message || "Processing...";
          } else {
            this.isProcessing = false;
            this.callResult = res as CallSummary;
            this.pollingSub?.unsubscribe();
            this.fetchTranscript(this.callResult.call_id);
          }
        },
        error: () => {
          this.processingStatus = "Error checking status. Retrying...";
        },
      });
    });
  }

  fetchTranscript(callId: string) {
    this.uploadService.getTranscript(callId).subscribe({
      next: (res) => (this.transcriptResult = res as TranscriptResult),
      error: () => (this.transcriptResult = null),
    });
  }

  exportToPDF() {
    if (!this.callResult) return;
    const doc = new jsPDF();
    doc.setFontSize(16);
    doc.text("Call Analysis", 10, 10);
    doc.setFontSize(12);
    let y = 20;
    doc.text(`Call ID: ${this.callResult.call_id}`, 10, y);
    y += 8;
    doc.text(`Category: ${this.callResult.category}`, 10, y);
    y += 8;
    doc.text(`Sentiment: ${this.callResult.sentiment}`, 10, y);
    y += 8;
    doc.text(`Priority: ${this.callResult.priority}`, 10, y);
    y += 8;
    doc.text(`Resolution: ${this.callResult.resolution_status}`, 10, y);
    y += 8;
    doc.text(
      `Follow Up: ${
        this.callResult.follow_up_required ? "Required" : "Not Required"
      }`,
      10,
      y
    );
    y += 8;
    doc.text(
      `Processed At: ${new Date(
        this.callResult.processed_at
      ).toLocaleString()}`,
      10,
      y
    );
    y += 8;
    doc.text(`Tags: ${(this.callResult.tags || []).join(", ")}`, 10, y);
    y += 10;
    doc.text("Summary:", 10, y);
    y += 8;
    (this.callResult.summary || []).forEach((item, idx) => {
      doc.text(`- ${item}`, 15, y);
      y += 7;
    });
    y += 3;
    doc.text("Action Items:", 10, y);
    y += 8;
    (this.callResult.action_items || []).forEach((item, idx) => {
      doc.text(`- ${item}`, 15, y);
      y += 7;
    });
    y += 3;
    doc.text("Customer Requests:", 10, y);
    y += 8;
    (this.callResult.customer_requests || []).forEach((item, idx) => {
      doc.text(`- ${item}`, 15, y);
      y += 7;
    });
    y += 3;
    doc.text("Agent Performance:", 10, y);
    y += 8;
    doc.text(this.callResult.agent_performance, 15, y, { maxWidth: 180 });
    doc.save("call-analysis.pdf");
  }

  exportTranscriptToPDF() {
    if (!this.transcriptResult) return;
    const doc = new jsPDF();
    doc.setFontSize(16);
    doc.text("Call Transcript", 10, 10);
    doc.setFontSize(12);
    let y = 20;
    doc.text(`Call ID: ${this.transcriptResult.call_id}`, 10, y);
    y += 8;
    doc.text(
      `Audio Duration: ${this.transcriptResult.audio_duration} sec`,
      10,
      y
    );
    y += 8;
    doc.text(
      `Processed At: ${new Date(
        this.transcriptResult.processed_at
      ).toLocaleString()}`,
      10,
      y
    );
    y += 10;
    doc.text("Transcript:", 10, y);
    y += 8;
    doc.setFont("courier", "normal");
    doc.setFontSize(10);
    const transcriptLines = this.transcriptResult.transcript.split("\n");
    transcriptLines.forEach((line) => {
      doc.text(line, 10, y, { maxWidth: 190 });
      y += 6;
      if (y > 280) {
        doc.addPage();
        y = 10;
      }
    });
    doc.save("call-transcript.pdf");
  }

  ngOnDestroy() {
    this.pollingSub?.unsubscribe();
  }
}
