import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UseRawMaterialComponent } from './use-raw-material.component';

describe('UseRawMaterialComponent', () => {
  let component: UseRawMaterialComponent;
  let fixture: ComponentFixture<UseRawMaterialComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ UseRawMaterialComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(UseRawMaterialComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
