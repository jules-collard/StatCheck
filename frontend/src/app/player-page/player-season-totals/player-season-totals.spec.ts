import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PlayerSeasonTotals } from './player-season-totals';

describe('PlayerSeasonTotals', () => {
  let component: PlayerSeasonTotals;
  let fixture: ComponentFixture<PlayerSeasonTotals>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PlayerSeasonTotals]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PlayerSeasonTotals);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
