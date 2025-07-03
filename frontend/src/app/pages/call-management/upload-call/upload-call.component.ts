import { Component, ViewChild, ElementRef, OnDestroy } from "@angular/core";

import { interval, Subscription } from "rxjs";
import jsPDF from "jspdf";
import {UploadCallService} from "../../../services/upload-call.service";
import {MatCardModule} from "@angular/material/card";
import {MatButtonModule} from "@angular/material/button";
import {MatIconModule} from "@angular/material/icon";
import {MatProgressBarModule} from "@angular/material/progress-bar";
import {MatProgressSpinnerModule} from "@angular/material/progress-spinner";
import {MatDividerModule} from "@angular/material/divider";
import {MatListModule} from "@angular/material/list";
import {MatChipsModule} from "@angular/material/chips";
import {CommonModule} from "@angular/common";

@Component({
  selector: "app-upload-call",
  imports : [MatCardModule
    ,MatButtonModule
    ,MatIconModule
    ,MatProgressBarModule
    ,MatProgressSpinnerModule
    ,MatListModule
    ,MatDividerModule,
      MatChipsModule,
      CommonModule
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
  processingStatus = "";
  callResult: any = null;

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
            this.callResult = res;
            this.pollingSub?.unsubscribe();
          }
        },
        error: () => {
          this.processingStatus = "Error checking status. Retrying...";
        },
      });
    });
  }

  exportToPDF() {
    if (!this.callResult) return;
    const doc = new jsPDF();
    doc.setFontSize(16);
    doc.text("Call Transcript", 10, 10);
    doc.setFontSize(12);
    doc.text(`Customer: ${this.callResult.customerName}`, 10, 20);
    doc.text(`Agent: ${this.callResult.agentName}`, 10, 28);
    doc.text(
      `Date: ${new Date(this.callResult.timestamp).toLocaleString()}`,
      10,
      36
    );
    doc.text(`Duration: ${this.callResult.duration} seconds`, 10, 44);
    doc.text(`Sentiment: ${this.callResult.sentiment}`, 10, 52);
    doc.text(`Rating: ${this.callResult.rating}/10`, 10, 60);
    doc.text("Summary:", 10, 70);
    doc.text(this.callResult.summary, 10, 78, { maxWidth: 190 });
    doc.text("Action Items:", 10, 90);
    (this.callResult.actionItems || []).forEach((item: string, idx: number) => {
      doc.text(`- ${item}`, 15, 98 + idx * 8);
    });
    doc.text(
      "Transcript:",
      10,
      110 + (this.callResult.actionItems?.length || 0) * 8
    );
    doc.setFont("courier", "normal");
    doc.setFontSize(10);
    doc.text(
      this.callResult.transcript,
      10,
      118 + (this.callResult.actionItems?.length || 0) * 8,
      { maxWidth: 190 }
    );
    doc.save("call-transcript.pdf");
  }

  ngOnDestroy() {
    this.pollingSub?.unsubscribe();
  }
}
