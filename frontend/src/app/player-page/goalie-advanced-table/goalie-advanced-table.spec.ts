import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GoalieAdvancedTable } from './goalie-advanced-table';

describe('GoalieAnalyticsTable', () => {
  let component: GoalieAdvancedTable;
  let fixture: ComponentFixture<GoalieAdvancedTable>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [GoalieAdvancedTable]
    })
    .compileComponents();

    fixture = TestBed.createComponent(GoalieAdvancedTable);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
