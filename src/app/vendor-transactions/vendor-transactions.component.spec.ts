import { ComponentFixture, TestBed } from '@angular/core/testing';

import { VendorTransactionsComponent } from './vendor-transactions.component';

describe('VendorTransactionsComponent', () => {
  let component: VendorTransactionsComponent;
  let fixture: ComponentFixture<VendorTransactionsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ VendorTransactionsComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(VendorTransactionsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
