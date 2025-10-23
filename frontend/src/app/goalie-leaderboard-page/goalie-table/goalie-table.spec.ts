import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GoalieTable } from './goalie-table';

describe('GoalieTable', () => {
  let component: GoalieTable;
  let fixture: ComponentFixture<GoalieTable>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [GoalieTable]
    })
    .compileComponents();

    fixture = TestBed.createComponent(GoalieTable);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
