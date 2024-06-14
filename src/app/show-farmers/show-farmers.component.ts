import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-show-farmers',
  templateUrl: './show-farmers.component.html',
  styleUrls: ['./show-farmers.component.scss']
})
export class ShowFarmersComponent implements OnInit {
  data: any[] = [];
  columns: string[] = ['token_id', 'name', 'mobno', 'accno', 'ifsc', 'branch', 'net_amount'];

  constructor(private http: HttpClient) { }

  ngOnInit(): void {
    this.fetchData();
  }

  fetchData(): void {
    this.http.get<any[]>('http://127.0.0.1:5000/api/data')
      .subscribe(response => {
        this.data = response;
      }, error => {
        console.error('Error fetching data', error);
      });
  }
}