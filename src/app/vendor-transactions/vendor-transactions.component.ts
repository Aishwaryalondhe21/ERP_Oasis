import { Component } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Component({
  selector: 'app-vendor-transactions',
  templateUrl: './vendor-transactions.component.html',
  styleUrls: ['./vendor-transactions.component.scss']
})
export class VendorTransactionsComponent {
  vendorId: string = '';
  tableData: any[] = [];
  columnNames: string[] = [];

  constructor(private http: HttpClient) {}

  onVendorIdInput(event: Event) {
    const input = event.target as HTMLInputElement;
    this.vendorId = input.value;
  }

  onSubmit(event: Event) {
    event.preventDefault();
    this.fetchData();
  }

  fetchData() {
    if (this.vendorId) {
      const headers = new HttpHeaders({ 'Content-Type': 'application/json' });
      this.http.post<any>('http://127.0.0.1:5000/VendorTransaction', { vendor_id: this.vendorId }, { headers }).subscribe(
        data => {
          console.log('Data received:', data); // Debug: Check the received data
          if (Array.isArray(data)) {
            this.columnNames = Object.keys(data[0]);
            this.tableData = data;
            console.log('Column Names:', this.columnNames); // Debug: Check column names
            console.log('Table Data:', this.tableData); // Debug: Check table data
          } else {
            alert(data.error || 'Unknown error');
          }
        },
        error => {
          console.error('Error:', error);
          alert(`An error occurred while fetching data: ${error.message || error.error || 'Unknown error'}`);
        }
      );
    } else {
      alert('Please enter a vendor ID');
    }
  }
}
