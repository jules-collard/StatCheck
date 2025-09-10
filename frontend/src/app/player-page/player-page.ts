import { Component, computed, DestroyRef, inject, OnInit, signal } from '@angular/core';

import { PlayerDetails } from "./player-details/player-details";
import { PlayerService } from './player.service';
import { ActivatedRoute } from '@angular/router';
import { SkaterStats } from './skater-stats.model';
import { Player } from './player.model';
import { Award } from './award.model';
import { SeasonTotalsTable } from './season-totals-table/season-totals-table';
import { GoalieTotalsTable } from "./goalie-totals-table/goalie-totals-table";
import { GoalieStats } from './goalie-stats.model';
import { SeasonAnalyticsTable } from './season-analytics-table/season-analytics-table';
import { GoalieAdvancedTable } from './goalie-advanced-table/goalie-advanced-table';

@Component({
  selector: 'app-player-page',
  imports: [PlayerDetails, SeasonTotalsTable, GoalieTotalsTable, SeasonAnalyticsTable, GoalieAdvancedTable],
  templateUrl: './player-page.html',
  styleUrl: './player-page.css'
})
export class PlayerPage implements OnInit {
  private playerService = inject(PlayerService);
  private activatedRoute = inject(ActivatedRoute);
  private destroyRef = inject(DestroyRef);

  playerData = computed<Player | null>(() => {
    return this.playerService.getPlayerData();
  })

  regularSeason = signal<boolean>(true)

  stats = computed<SkaterStats[] | GoalieStats[] | null>(() => {
    if (this.regularSeason()) {
      return this.regSeasonTotals();
    } else { return this.postSeasonTotals()}
  })
  
  regSeasonTotals = computed<SkaterStats[] | GoalieStats[] | null>(() => {
    let totals = this.playerService.getRegSeasonStats();
    if (totals != null && totals.length > 0) {
      if ('goals' in totals[0]) { // Check SeasonTotals[]
        const records = this.playerService.getSkaterRecords()
        return (totals as SkaterStats[]).map((stats) => {
          stats.totals.records = records?.find((record) => record.season === stats.season);
          return stats;
        })
      } else { // GoalieTotals[]
        const records = this.playerService.getGoalieRecords()
        return (totals as GoalieStats[]).map((stats) => {
          stats.totals.records = records?.find((record) => record.season === stats.season);
          return stats;
        })
      }
    }
    return totals;
  })

  postSeasonTotals = computed<SkaterStats[] | GoalieStats[] | null>(() => {
    return this.playerService.getPostSeasonStats();
  })

  awards = computed<Award[]>(() => {
    return this.playerData()?.awards.filter((award) => {
      return this.awardNames.includes(award.awardName)
    }) ?? [];
  })

  loading = computed<boolean>(() => {
    return this.playerService.playerDataIsLoading() || this.playerService.seasonStatsIsLoading()
  })

  private awardNames = ['Vezina Trophy', 'Hart Memorial Trophy', 'Calder Memorial Trophy', 'James Norris Memorial Trophy', 'Frank J. Selke Trophy', 'Conn Smythe Trophy', 'Stanley Cup']

  selectPlayoffs() {
    this.regularSeason.set(false)
  }

  selectRegular() {
    this.regularSeason.set(true)
  }

  ngOnInit(): void {
    const subscription = this.activatedRoute.paramMap.subscribe({
      next: (paramMap) => {
        this.playerService.setPlayerID(Number(paramMap.get('playerID')))
      }
    })

    this.destroyRef.onDestroy(() => subscription.unsubscribe())
  }

}
