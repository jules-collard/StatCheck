import { Component, computed, effect, inject, input as routeBinding, signal } from '@angular/core';
import { Router } from '@angular/router';
import { GlobalConfigService } from '../shared/global-config.service';
import { ListConfig, PlayerListService } from '../shared/player-list/player-list.service';
import { GoalieLeaderboardItem } from './goalie-leaderboard-item.model';
import { SortConfig, TableSortService } from '../shared/table-sort.service';
import { GoalieTable } from "./goalie-table/goalie-table";
import { SeasonPipe } from '../pipes/season.pipe';
import { PlayerListButton } from '../shared/player-list/player-list-button/player-list-button';
import { PlayerFilter } from '../shared/player-list/player-filter/player-filter';

@Component({
  selector: 'app-goalie-leaderboard-page',
  imports: [GoalieTable, SeasonPipe, PlayerListButton, PlayerFilter],
  templateUrl: './goalie-leaderboard-page.html',
  styleUrl: './goalie-leaderboard-page.css',
  providers: [PlayerListService, TableSortService]
})
export class GoalieLeaderboardPage {
  // Menu Navigation
  globalConfig = inject(GlobalConfigService);
  router = inject(Router);
  seasonsList = this.globalConfig.seasons.sort((a, b) => b - a);

  navigateSeason(season: number) {
    this.sortService.reset();
    this.router.navigate(['leaderboards', season, 'goalies']);
  }
  
  // Leaderboard Setup
  listService = inject(PlayerListService<GoalieLeaderboardItem>);

  season = routeBinding.required<number>();
  gameType = signal<2|3>(2);

  config = computed<ListConfig>(() => {
    const config: ListConfig = {
      type: 'leaderboard',
      itemsPerPage: 16,
      leaderboardConfig: {
        season: this.season(),
        playerType: 'goalies',
        gameType: this.gameType()
      }
    }
    return config
  })

  configEffect = effect(() => {
    this.listService.setConfig(this.config())
  })

  goalies = computed<GoalieLeaderboardItem[]>(() => this.listService.slicedPlayers())

  // Sorting
  private sortService = inject(TableSortService<GoalieLeaderboardItem>);

  sortingEffect = effect(() => {
    const sortConfig: SortConfig<GoalieLeaderboardItem> = {
      gamesPlayed: item => item.totals.gamesPlayed,
      gamesStarted: item => item.totals.gamesStarted,
      wins: item => item.totals.wins,
      losses: item => item.totals.losses,
      goalsAgainstAvg: item => item.totals.goalsAgainstAvg,
      savePct: item => item.totals.savePct ?? 0,
      goalsSavedAx: (item) => item.advanced.xgAgainst - item.advanced.xgGoalsAgainst,
      deltaFenwick: (item) => (item.advanced.xgAgainst - item.advanced.xgGoalsAgainst) / item.advanced.fenwickAgainst,
      evSavePct: (item) => item.totals.evenStrengthSavePct ?? 0,
      ppSavePct: (item) => item.totals.powerPlaySavePct ?? 0
    }
    this.sortService.setSortConfig(sortConfig);
  })
}
