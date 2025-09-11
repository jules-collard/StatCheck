import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SkaterTotalsTable } from './skater-totals-table';

describe('SeasonTotalsTable', () => {
  let component: SkaterTotalsTable;
  let fixture: ComponentFixture<SkaterTotalsTable>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SkaterTotalsTable]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SkaterTotalsTable);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
