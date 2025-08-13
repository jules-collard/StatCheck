import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SeasonTotalsTable } from './season-totals-table';

describe('SeasonTotalsTable', () => {
  let component: SeasonTotalsTable;
  let fixture: ComponentFixture<SeasonTotalsTable>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SeasonTotalsTable]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SeasonTotalsTable);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
