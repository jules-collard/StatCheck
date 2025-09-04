import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GoalieAnalyticsTable } from './goalie-analytics-table';

describe('GoalieAnalyticsTable', () => {
  let component: GoalieAnalyticsTable;
  let fixture: ComponentFixture<GoalieAnalyticsTable>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [GoalieAnalyticsTable]
    })
    .compileComponents();

    fixture = TestBed.createComponent(GoalieAnalyticsTable);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
