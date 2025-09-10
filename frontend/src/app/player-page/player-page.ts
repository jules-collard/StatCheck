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
import { SkaterOnIceTable } from "./skater-onice-table/skater-onice-table";

@Component({
  selector: 'app-player-page',
  imports: [PlayerDetails, SeasonTotalsTable, GoalieTotalsTable, SeasonAnalyticsTable, GoalieAdvancedTable, SkaterOnIceTable],
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
    return this.playerService.getRegSeasonStats()
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
