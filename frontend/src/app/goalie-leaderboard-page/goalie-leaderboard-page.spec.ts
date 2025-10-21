import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GoalieLeaderboardPage } from './goalie-leaderboard-page';

describe('GoalieLeaderboardPage', () => {
  let component: GoalieLeaderboardPage;
  let fixture: ComponentFixture<GoalieLeaderboardPage>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [GoalieLeaderboardPage]
    })
    .compileComponents();

    fixture = TestBed.createComponent(GoalieLeaderboardPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
