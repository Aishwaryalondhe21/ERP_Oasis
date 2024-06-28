import { Component, OnInit } from '@angular/core';


import { HttpClient } from '@angular/common/http';
@Component({
  selector: 'app-raw-materials-deatails',
  templateUrl: './raw-materials-deatails.component.html',
  styleUrls: ['./raw-materials-deatails.component.scss']
})
export class RawMaterialsDeatailsComponent implements OnInit {

  data: any[] = [];
  columns: string[] = ['buydate', 'MilkCM500RoleQuan', 'MilkCM500RolePrice', 'MilkCM200RoleQuan', 'MilkCM200RolePrice',
        'MilkTM500RoleQuan', 'MilkTM500RolePrice', 'MilkTM200RoleQuan', 'MilkTM200RolePrice',
        'Lassi200RoleQuan', 'Lassi200RolePrice', 'LassiCUP200cupQuan', 'LassiCUP200cupPrice',
        'LassiMANGOCUP200cupQuan', 'LassiMANGOCUP200cupPrice', 'Dahi200MLRoleQuan', 'Dahi200MLRolePrice',
        'Dahi500MLRoleQuan', 'Dahi500MLRolePrice', 'Dahi2LTBucketQuan', 'Dahi2LTBucketPrice',
        'Dahi5LTBucketQuan', 'Dahi5LTBucketPrice', 'Dahi10LTBucketQuan', 'Dahi10LTBucketPrice',
        'Dahi2LT1_5BucketQuan', 'Dahi2LT1_5BucketPrice', 'Dahi5LT1_5BucketQuan', 'Dahi5LT1_5BucketPrice',
        'Dahi10LT1_5BucketQuan', 'Dahi10LT1_5BucketPrice', 'ButtermilkRoleQuan', 'ButtermilkRolePrice',
        'Khova500TinQuan', 'Khova500TinPrice', 'Khoya1000TinQuan', 'Khoya1000TinPrice',
        'Shrikhand100TinQuan', 'Shrikhand100TinPrice', 'Shrikhand250TinQuan', 'Shrikhand250TinPrice',
        'Ghee200TinQuan', 'Ghee200TinPrice', 'Ghee500TinQuan', 'Ghee500TinPrice',
        'Ghee15LTTinQuan', 'Ghee15LTTinPrice', 'PaneerlooseQuan', 'PaneerloosePrice',
        'khovalooseQuan', 'khovaloosePrice', 'LASSICUPFOILQuan', 'LASSICUPFOILPrice',
        'IFFFLAVERMANGOQuan', 'IFFFLAVERMANGOPrice', 'IFFFLAVERVANILLAQuan', 'IFFFLAVERVANILLAPrice',
        'CULTUREAMAZIKAQuan', 'CULTUREAMAZIKAPrice', 'CULTUREDANISKOQuan', 'CULTUREDANISKOPrice',
        'CULTUREHRQuan', 'CULTUREHRPrice', 'LIQUIDSOAPQuan', 'LIQUIDSOAPPrice',
        'COSSODAQuan', 'COSSODAPrice', 'KAOHQuan', 'KAOHPrice'];

  constructor(private http: HttpClient) { }

  ngOnInit(): void {
    this.fetchData();
  }
  fetchData(): void {
    this.http.get<any[]>('http://127.0.0.1:5000//show_raw_materials')
      .subscribe(response => {
        this.data = response;
      }, error => {
        console.error('Error fetching data', error);
      });

}
}
