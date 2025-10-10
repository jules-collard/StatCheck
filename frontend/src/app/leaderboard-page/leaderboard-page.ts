import { Component, computed, effect, inject, input, signal, OnInit } from '@angular/core';
import { SkaterLeaderboardItem } from './skater-leaderboard-item.model';
import { ListConfig, LeaderboardConfig, PlayerListService } from '../shared/player-list.service';
import { SkaterTable } from './skater-table/skater-table';

@Component({
  selector: 'app-leaderboard-page',
  imports: [SkaterTable],
  templateUrl: './leaderboard-page.html',
  styleUrl: './leaderboard-page.css',
  providers: [PlayerListService]
})
export class LeaderboardPage implements OnInit {
  private listService = inject(PlayerListService<SkaterLeaderboardItem>);
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

  leaderboard = computed<SkaterLeaderboardItem[]>(() => this.listService.filteredPlayers());

  ngOnInit(): void {
    const listConfig: ListConfig = {
      type: 'leaderboard',
      leaderboardConfig: {
        season: this.season(),
        playerType: this.playerType(),
        gameType: this.gameType()
      }
    }
    this.listService.setConfig(listConfig);
  }
}
