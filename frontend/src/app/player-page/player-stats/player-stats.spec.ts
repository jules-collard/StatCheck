import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SeasonStats } from './season-stats';

describe('SeasonStats', () => {
  let component: SeasonStats;
  let fixture: ComponentFixture<SeasonStats>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SeasonStats]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SeasonStats);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
