import { ComponentFixture, TestBed } from '@angular/core/testing';

import { VendorPaymentsComponent } from './vendor-payments.component';

describe('VendorPaymentsComponent', () => {
  let component: VendorPaymentsComponent;
  let fixture: ComponentFixture<VendorPaymentsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ VendorPaymentsComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(VendorPaymentsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
