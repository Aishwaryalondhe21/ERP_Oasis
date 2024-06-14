import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-show-vendors',
  templateUrl: './show-vendors.component.html',
  styleUrls: ['./show-vendors.component.scss']
})
export class ShowVendorsComponent implements OnInit {
  data: any[] = [];
  columns: string[] = ['token', 'name', 'enterprise', 'gstno', 'address', 'mobno','amount'];

  constructor(private http: HttpClient) { }

  ngOnInit(): void {
    this.fetchData();
  }

  fetchData(): void {
    this.http.get<any[]>('http://127.0.0.1:5000/showven')
      .subscribe(response => {
        this.data = response;
      }, error => {
        console.error('Error fetching data', error);
      });
    }

}
