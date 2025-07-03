import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LiveCallComponent } from './live-call.component';

describe('LiveCallComponent', () => {
  let component: LiveCallComponent;
  let fixture: ComponentFixture<LiveCallComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [LiveCallComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(LiveCallComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
