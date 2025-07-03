import { Injectable } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { Observable } from "rxjs";

@Injectable({ providedIn: "root" })
export class UploadCallService {
  private baseUrl = "http://localhost:8000/api/v1"; // Change to your FastAPI base URL

  constructor(private http: HttpClient) {}

  uploadCall(file: File): Observable<any> {
    const formData = new FormData();
    formData.append("audio_file", file);
    return this.http.post<any>(`${this.baseUrl}/upload`, formData);
  }

  getProcessingStatus(processingUrl: string): Observable<any> {
    // If the backend returns a relative URL, prepend the base URL
    const url = processingUrl.startsWith("http")
      ? processingUrl
      : `http://localhost:8000${processingUrl}`;
    return this.http.get<any>(url);
  }

  getTranscript(processingUrl: string): Observable<any> {
    // If the backend returns a relative URL, prepend the base URL
    const url = processingUrl.startsWith("http")
      ? processingUrl
      : `http://localhost:8000${processingUrl}`;
    return this.http.get<any>(url);
  }
}
