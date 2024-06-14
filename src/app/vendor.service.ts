import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { FormsModule } from '@angular/forms';

@Injectable({
  providedIn: 'root'
})
export class VendorService {
  private baseUrl = 'http://localhost:5000'; // Adjust this to match your Flask server's URL

  constructor(private http: HttpClient) { }

  getAmount(vendorId: string): Observable<any> {
    return this.http.post<any>(`${this.baseUrl}/get_amount`, { vendorId });
  }

  updateAmount(vendorId: string, paidAmount: number): Observable<any> {
    return this.http.post<any>(`${this.baseUrl}/update_amount`, { vendorId, paidAmount });
  }
}
