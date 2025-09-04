import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SeasonAnalyticsTable } from './season-analytics-table';

describe('SeasonAnalyticsTable', () => {
  let component: SeasonAnalyticsTable;
  let fixture: ComponentFixture<SeasonAnalyticsTable>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SeasonAnalyticsTable]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SeasonAnalyticsTable);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
