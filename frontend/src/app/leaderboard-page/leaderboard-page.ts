import { Component, computed, effect, inject, input, signal } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { LeaderboardConfig, LeaderboardService } from './leaderboard.service';
import { SkaterLeaderboardItem } from './skater-leaderboard-item.model';

@Component({
  selector: 'app-leaderboard-page',
  imports: [],
  templateUrl: './leaderboard-page.html',
  styleUrl: './leaderboard-page.css',
  providers: [LeaderboardService]
})
export class LeaderboardPage {
  private leaderboardService = inject(LeaderboardService);
  season = input.required<number>();
  playerType = signal<'skaters'|'goalies'>('skaters');
  gameType = signal<2|3>(2);

  config = computed<LeaderboardConfig>(() => {
    const config: LeaderboardConfig = {
      season: this.season(),
      playerType: this.playerType(),
      gameType: this.gameType()
    }
    return config
  })

  configEffect = effect(() => {
    this.leaderboardService.setConfig(this.config())
  })

  leaderboard = computed<SkaterLeaderboardItem[]>(() => this.leaderboardService.getLeaderboard())
}
