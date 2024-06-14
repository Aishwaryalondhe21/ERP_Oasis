import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';


@Component({
  selector: 'app-vendor-status',
  templateUrl: './vendor-status.component.html',
  styleUrls: ['./vendor-status.component.scss']
})
export class VendorStatusComponent implements OnInit {
  data: any[] = [];
  columns: string[] = [
    'name', 'vendorId', 'MilkCM500Price', 'MilkCM200Price', 'MilkTM500Price', 'MilkTM200Price', 
    'Lassi200Price', 'LassiCUP200Price', 'LassiMANGOCUP200Price', 'Dahi200Price', 'Dahi500Price', 
    'Dahi2LTPrice', 'Dahi5LTPrice', 'Dahi10LTPrice', 'Dahi2LTPrice15', 'Dahi5LTPrice15', 
    'Dahi10LTPrice15', 'ButtermilkPrice', 'Khova500Price', 'Khoya1000Price', 'Shrikhand100Price', 
    'Shrikhand250Price', 'Ghee200Price', 'Ghee500Price', 'Ghee15LTPrice', 'PaneerloosePrice', 
    'khovaloosePrice'];

  constructor(private http: HttpClient) { }

  ngOnInit(): void {
    this.fetchData();
  }

  fetchData(): void {
    this.http.get<any[]>('http://127.0.0.1:5000/VendorStatus')
      .subscribe(response => {
        this.data = response;
      }, error => {
        console.error('Error fetching data', error);
      });
    }


}
