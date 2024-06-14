import { Component } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Component({
  selector: 'app-vendor-payments',
  templateUrl: './vendor-payments.component.html',
  styleUrls: ['./vendor-payments.component.scss']
})
export class VendorPaymentsComponent {
  vendorId: number | null = null;
  amount: number | null = null;
  paidAmount: number | null = null;

  constructor(private http: HttpClient) {}

  showAmount(event: Event) {
    event.preventDefault();
    if (this.vendorId !== null) {
      const headers = new HttpHeaders({ 'Content-Type': 'application/json' });
      console.log('Sending vendor ID:', this.vendorId);
      this.http.post<any>('http://localhost:5000/get_vendor', { vendorId: this.vendorId }, { headers }).subscribe(
        data => {
          console.log('Received response:', data);
          if (data.amount !== undefined) {
            this.amount = data.amount;
            console.log('Updated amount:', this.amount);
          } else {
            alert('Vendor not found');
          }
        },
        error => {
          console.error('Error:', error);
        }
      );
    }
  }
  
  submitPayment(event: Event) {
    event.preventDefault();
    if (this.vendorId !== null && this.paidAmount !== null) {
      const headers = new HttpHeaders({ 'Content-Type': 'application/json' });
      console.log('Sending vendor ID and paid amount:', this.vendorId, this.paidAmount);
      this.http.post<any>('http://localhost:5000/update_vendor', { vendorId: this.vendorId, paidAmount: this.paidAmount }, { headers }).subscribe(
        data => {
          console.log('Received response:', data);
          if (data.new_amount !== undefined) {
            this.amount = data.new_amount;
            console.log('Updated amount:', this.amount);
            alert('Payment successful');
          } else {
            alert('Vendor not found');
          }
        },
        error => {
          console.error('Error:', error);
        }
      );
    }
  }
}
