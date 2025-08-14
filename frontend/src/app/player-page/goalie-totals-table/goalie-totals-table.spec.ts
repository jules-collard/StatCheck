import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GoalieTotalsTable } from './goalie-totals-table';

describe('GoalieTotalsTable', () => {
  let component: GoalieTotalsTable;
  let fixture: ComponentFixture<GoalieTotalsTable>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [GoalieTotalsTable]
    })
    .compileComponents();

    fixture = TestBed.createComponent(GoalieTotalsTable);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
