import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ShowVendorsComponent } from './show-vendors.component';

describe('ShowVendorsComponent', () => {
  let component: ShowVendorsComponent;
  let fixture: ComponentFixture<ShowVendorsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ShowVendorsComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ShowVendorsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
