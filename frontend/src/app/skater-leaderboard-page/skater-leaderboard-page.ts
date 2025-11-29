import { Component, computed, inject, input as routeBinding, signal, effect } from '@angular/core';
import { Router } from '@angular/router';

import { SkaterLeaderboardItem } from './skater-leaderboard-item.model';
import { ListConfig, PlayerListService } from '../shared/player-list/player-list.service';
import { SkaterTable } from './skater-table/skater-table';
import { PlayerListButton } from "../shared/player-list/player-list-button/player-list-button";
import { PlayerFilter } from '../shared/player-list/player-filter/player-filter';
import { GlobalConfigService } from '../shared/global-config.service';
import { SeasonPipe } from '../pipes/season.pipe';
import { SortConfig, TableSortService } from '../shared/table-sort.service';
import { ShootingTable } from "./shooting-table/shooting-table";
import { OnIceTable } from "./on-ice-table/on-ice-table";

@Component({
  selector: 'app-leaderboard-page',
  imports: [SkaterTable, PlayerListButton, PlayerFilter, SeasonPipe, ShootingTable, OnIceTable],
  templateUrl: './skater-leaderboard-page.html',
  styleUrl: './skater-leaderboard-page.css',
  providers: [PlayerListService, TableSortService]
})
export class SkaterLeaderboardPage {
  router = inject(Router)
  globalConfig = inject(GlobalConfigService);

  listService = inject(PlayerListService<SkaterLeaderboardItem>);
  private sortService = inject(TableSortService<SkaterLeaderboardItem>);

  currentTab = signal<'totals' | 'shooting' | 'onice'>('totals')
  shootingTab = computed<boolean>(() => this.currentTab() === 'shooting')
  
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
      itemsPerPage: 15,
      leaderboardConfig: {
        season: this.season(),
        playerType: this.playerType(),
        gameType: this.gameType(),
        shotsFilter: this.shootingTab()
      }
    }
    return config
  })

  configEffect = effect(() => {
    this.listService.setConfig(this.config())
  })

  navigateSeason(season: number) {
    this.sortService.reset();
    this.router.navigate(['leaderboards', season, 'skaters']);
  }

  // Sorting
  sortingEffect = effect(() => {
    const sortConfig: SortConfig<SkaterLeaderboardItem> = {
      gamesPlayed: (item) => item.totals.gamesPlayed,
      goals: (item) => item.totals.goals,
      assists: (item) => item.totals.assists,
      points: (item) => item.totals.goals + item.totals.assists,
      plusMinus: (item) => item.totals.plusMinus,
      sog: (item) => item.totals.sog,
      hits: (item) => item.totals.hits,
      blocks: (item) => item.totals.blocks,
      penaltyMinutes: (item) => item.totals.penaltyMinutes,
      avgTOI: (item) => item.totals.avgTOI,
      goalsAx: (item) => item.shooting.xgGoals - item.shooting.xg,
      shootingPct: (item) => item.totals.goals / item.totals.sog,
      deltaFenwick: (item) => (item.shooting.xgGoals - item.shooting.xg) / item.shooting.fenwick,
      corsiFor: (item) => item.onIce.corsiFor / (item.onIce.corsiFor + item.onIce.corsiAgainst),
      fenwickFor: (item) => item.onIce.fenwickFor / (item.onIce.fenwickFor + item.onIce.fenwickAgainst),
      xgFor: (item) => item.onIce.xgFor / (item.onIce.xgFor + item.onIce.xgAgainst),
      onIceShootingPct: (item) => item.onIce.onIceShootingPct,
      oZoneStarts: (item) => item.onIce.oZoneStarts / (item.onIce.oZoneStarts + item.onIce.nZoneStarts + item.onIce.dZoneStarts),
      dZoneStarts: (item) => item.onIce.dZoneStarts / (item.onIce.oZoneStarts + item.onIce.nZoneStarts + item.onIce.dZoneStarts)
    }
    this.sortService.setSortConfig(sortConfig);
  })
}
