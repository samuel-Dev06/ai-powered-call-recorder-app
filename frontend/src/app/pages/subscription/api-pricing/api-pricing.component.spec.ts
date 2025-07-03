import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ApiPricingComponent } from './api-pricing.component';

describe('ApiPricingComponent', () => {
  let component: ApiPricingComponent;
  let fixture: ComponentFixture<ApiPricingComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ApiPricingComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ApiPricingComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
