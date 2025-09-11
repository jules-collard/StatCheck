import { Component, computed, DestroyRef, inject, OnInit, signal } from '@angular/core';

import { PlayerDetails } from "./player-details/player-details";
import { PlayerService } from './player.service';
import { ActivatedRoute } from '@angular/router';
import { SkaterStats } from './skater-stats.model';
import { Player } from './player.model';
import { Award } from './award.model';
import { SkaterTotalsTable } from './skater-totals-table/skater-totals-table';
import { GoalieTotalsTable } from "./goalie-totals-table/goalie-totals-table";
import { GoalieStats } from './goalie-stats.model';
import { SeasonAnalyticsTable } from './season-analytics-table/season-analytics-table';
import { GoalieAdvancedTable } from './goalie-advanced-table/goalie-advanced-table';
import { SkaterOnIceTable } from "./skater-onice-table/skater-onice-table";

@Component({
  selector: 'app-player-page',
  imports: [PlayerDetails, SkaterTotalsTable, GoalieTotalsTable, SeasonAnalyticsTable, GoalieAdvancedTable, SkaterOnIceTable],
  templateUrl: './player-page.html',
  styleUrl: './player-page.css'
})
export class PlayerPage implements OnInit {
  private playerService = inject(PlayerService);
  private activatedRoute = inject(ActivatedRoute);
  private destroyRef = inject(DestroyRef);

  regularSeason = signal<boolean>(true)

  private awardNames = ['Vezina Trophy', 'Hart Memorial Trophy', 'Calder Memorial Trophy', 'James Norris Memorial Trophy', 'Frank J. Selke Trophy', 'Conn Smythe Trophy', 'Stanley Cup']

  playerData = computed<Player | null>(() => {
    return this.playerService.playerData.hasValue() ? this.playerService.playerData.value() : null;
  })

  stats = computed<SkaterStats[] | GoalieStats[] | null>(() => {
    return this.regularSeason() ? this.regSeasonStats() : this.postSeasonStats()
  })
  
  regSeasonStats = computed<SkaterStats[] | GoalieStats[] | null>(() => {
    return this.playerService.regSeasonStats.hasValue() ? this.playerService.regSeasonStats.value() : null;
  })

  postSeasonStats = computed<SkaterStats[] | GoalieStats[] | null>(() => {
    return this.playerService.postSeasonStats.hasValue() ? this.playerService.postSeasonStats.value() : null;
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

  ngOnInit(): void {
    const subscription = this.activatedRoute.paramMap.subscribe({
      next: (paramMap) => {
        this.playerService.setPlayerID(Number(paramMap.get('playerID')))
        this.playerService.fetch()
      }
    })

    this.destroyRef.onDestroy(() => subscription.unsubscribe())
  }

}
