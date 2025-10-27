import { Component, computed, effect, inject, input as routeBinding, signal } from '@angular/core';

import { PlayerDetails } from "./player-details/player-details";
import { SkaterStats } from './skater-stats.model';
import { Player } from './player.model';
import { Award } from './award.model';
import { SkaterTotalsTable } from './skater-totals-table/skater-totals-table';
import { GoalieTotalsTable } from "./goalie-totals-table/goalie-totals-table";
import { GoalieStats } from './goalie-stats.model';
import { SkaterAnalyticsTable } from './skater-analytics-table/skater-analytics-table';
import { GoalieAdvancedTable } from './goalie-advanced-table/goalie-advanced-table';
import { SkaterOnIceTable } from "./skater-onice-table/skater-onice-table";
import { PlayerService } from './player.service';

@Component({
  selector: 'app-player-page',
  imports: [PlayerDetails, SkaterTotalsTable, GoalieTotalsTable, SkaterAnalyticsTable, GoalieAdvancedTable, SkaterOnIceTable],
  templateUrl: './player-page.html',
  styleUrl: './player-page.css',
  providers: [PlayerService]
})
export class PlayerPage {
  playerID = routeBinding.required<number>();
  playerService = inject(PlayerService);

  idEffect = effect(() => {
    this.playerService.setPlayerID(this.playerID());
  })

  regularSeason = signal<boolean>(true);

  private awardNames = ['Vezina Trophy', 'Hart Memorial Trophy', 'Calder Memorial Trophy', 'James Norris Memorial Trophy', 'Frank J. Selke Trophy', 'Conn Smythe Trophy', 'Stanley Cup']

  playerData = computed<Player | null>(() => {
    if (this.playerService.playerData.hasValue()) {
      return this.playerService.playerData.value();
    } else {
      return null;
    }
  })

  regSeasonStats = computed<SkaterStats[] | GoalieStats[] | null>(() => {
    if (this.playerService.regSeasonStats.hasValue()) {
      return this.playerService.regSeasonStats.value();
    } else {
      return null;
    }
  })

  postSeasonStats = computed<SkaterStats[] | GoalieStats[] | null>(() => {
    if (this.playerService.postSeasonStats.hasValue()) {
      return this.playerService.postSeasonStats.value();
    } else {
      return null;
    }
  })

  stats = computed<SkaterStats[] | GoalieStats[] | null>(() => {
    return this.regularSeason() ? this.regSeasonStats() : this.postSeasonStats()
  })

  awards = computed<Award[]>(() => {
    return this.playerData()?.awards.filter((award) => {
      return this.awardNames.includes(award.awardName)
    }) ?? [];
  })

  selectPlayoffs() {
    this.regularSeason.set(false)
  }

  selectRegular() {
    this.regularSeason.set(true)
  }

}
