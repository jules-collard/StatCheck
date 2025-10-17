import { Component, computed, inject, input as routeBinding, signal, effect } from '@angular/core';
import { Router } from '@angular/router';

import { SkaterLeaderboardItem } from './skater-leaderboard-item.model';
import { ListConfig, PlayerListService } from '../shared/player-list/player-list.service';
import { SkaterTable } from './skater-table/skater-table';
import { PlayerListButton } from "../shared/player-list/player-list-button/player-list-button";
import { PlayerFilter } from '../shared/player-list/player-filter/player-filter';
import { GlobalConfigService } from '../shared/global-config.service';
import { SeasonPipe } from '../pipes/season.pipe';

@Component({
  selector: 'app-leaderboard-page',
  imports: [SkaterTable, PlayerListButton, PlayerFilter, SeasonPipe],
  templateUrl: './leaderboard-page.html',
  styleUrl: './leaderboard-page.css',
  providers: [PlayerListService]
})
export class LeaderboardPage {
  router = inject(Router)
  globalConfig = inject(GlobalConfigService);
  private listService = inject(PlayerListService<SkaterLeaderboardItem>);
  
  // Leaderboard properties
  season = routeBinding.required<number>();
  playerType = signal<'skaters'|'goalies'>('skaters');
  gameType = signal<2|3>(2);

  leaderboard = computed<SkaterLeaderboardItem[]>(() => this.listService.slicedPlayers());
  
  seasonsList = this.globalConfig.seasons.sort((a, b) => b - a);

  // Reactivity
  config = computed<ListConfig>(() => {
    const config: ListConfig = {
      type: 'leaderboard',
      itemsPerPage: 16,
      leaderboardConfig: {
        season: this.season(),
        playerType: this.playerType(),
        gameType: this.gameType()
      }
    }
    return config
  })

  configEffect = effect(() => {
    this.listService.setConfig(this.config())
  })

  navigateSeason(season: number) {
    this.router.navigate(['leaderboards', season]);
  }
}
