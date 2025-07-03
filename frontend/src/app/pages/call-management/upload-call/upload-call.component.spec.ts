import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UploadCallComponent } from './upload-call.component';

describe('UploadCallComponent', () => {
  let component: UploadCallComponent;
  let fixture: ComponentFixture<UploadCallComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [UploadCallComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(UploadCallComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
