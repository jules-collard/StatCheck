import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SkaterAnalyticsTable } from './skater-analytics-table';

describe('SeasonAnalyticsTable', () => {
  let component: SkaterAnalyticsTable;
  let fixture: ComponentFixture<SkaterAnalyticsTable>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SkaterAnalyticsTable]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SkaterAnalyticsTable);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
