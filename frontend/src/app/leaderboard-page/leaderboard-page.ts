import { Component, computed, inject, input, signal, OnInit } from '@angular/core';
import { SkaterLeaderboardItem } from './skater-leaderboard-item.model';
import { ListConfig, LeaderboardConfig, PlayerListService } from '../shared/player-list/player-list.service';
import { SkaterTable } from './skater-table/skater-table';
import { PlayerListButton } from "../shared/player-list/player-list-button/player-list-button";

@Component({
  selector: 'app-leaderboard-page',
  imports: [SkaterTable, PlayerListButton],
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

  leaderboard = computed<SkaterLeaderboardItem[]>(() => this.listService.slicedPlayers());

  ngOnInit(): void {
    const listConfig: ListConfig = {
      type: 'leaderboard',
      itemsPerPage: 16,
      leaderboardConfig: {
        season: this.season(),
        playerType: this.playerType(),
        gameType: this.gameType()
      }
    }
    this.listService.setConfig(listConfig);
  }
}
