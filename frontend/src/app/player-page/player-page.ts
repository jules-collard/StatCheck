import { Component, computed, DestroyRef, inject, OnInit, signal } from '@angular/core';

import { PlayerDetails } from "./player-details/player-details";
import { PlayerService } from './player.service';
import { ActivatedRoute } from '@angular/router';
import { SeasonTotals } from './season-totals-table/season-totals.model';
import { Player } from './player.model';
import { Award } from './award.model';
import { SeasonTotalsTable } from './season-totals-table/season-totals-table';
import { GoalieTotalsTable } from "./goalie-totals-table/goalie-totals-table";
import { GoalieTotals } from './goalie-totals-table/goalie-totals.model';
import { SkaterSeasonRecords } from './season-totals-table/skater-season-records.model';

@Component({
  selector: 'app-player-page',
  imports: [PlayerDetails, SeasonTotalsTable, GoalieTotalsTable],
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
  totals = computed<SeasonTotals[] | GoalieTotals[] | null>(() => {
    if (this.regularSeason()) {
      return this.regSeasonTotals();
    } else { return this.postSeasonTotals()}
  })
  
  regSeasonTotals = computed<SeasonTotals[] | GoalieTotals[] | null>(() => {
    let totals = this.playerService.getRegSeasonTotals();
    if (totals != null && totals.length > 0) {
      if ('goals' in totals[0]) { // Check SeasonTotals[]
        const records = this.playerService.getSkaterRecords()
        return (totals as SeasonTotals[]).map((total) => {
          total.records = records?.find((record) => record.season === total.season);
          return total;
        })
      } else { // GoalieTotals[]
        const records = this.playerService.getGoalieRecords()
        return (totals as GoalieTotals[]).map((total) => {
          total.records = records?.find((record) => record.season === total.season);
          return total;
        })
      }
    }
    return totals;
  })

  postSeasonTotals = computed<SeasonTotals[] | GoalieTotals[] | null>(() => {
    return this.playerService.getPostSeasonTotals();
  })

  awards = computed<Award[]>(() => {
    return this.playerData()?.awards.filter((award) => {
      return this.awardNames.includes(award.awardName)
    }) ?? [];
  })

  loading = computed<boolean>(() => {
    return this.playerService.playerDataIsLoading() || this.playerService.seasonTotalsIsLoading()
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
