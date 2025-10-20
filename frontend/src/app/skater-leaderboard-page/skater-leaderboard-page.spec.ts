import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SkaterLeaderboardPage } from './skater-leaderboard-page';

describe('LeaderboardPage', () => {
  let component: SkaterLeaderboardPage;
  let fixture: ComponentFixture<SkaterLeaderboardPage>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SkaterLeaderboardPage]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SkaterLeaderboardPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
