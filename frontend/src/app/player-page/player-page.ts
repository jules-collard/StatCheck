import { Component, computed, DestroyRef, inject, OnInit } from '@angular/core';

import { PlayerDetails } from "./player-details/player-details";
import { PlayerService } from './player.service';
import { ActivatedRoute } from '@angular/router';
import { SeasonTotals } from './player-season-totals/season-totals.model';
import { Player } from './player.model';
import { Award } from './award.model';
import { SeasonTotalsTable } from './season-totals-table/season-totals-table';

@Component({
  selector: 'app-player-page',
  imports: [PlayerDetails, SeasonTotalsTable],
  templateUrl: './player-page.html',
  styleUrl: './player-page.css'
})
export class PlayerPage implements OnInit {
  private playerService = inject(PlayerService);
  private activatedRoute = inject(ActivatedRoute);
  private destroyRef = inject(DestroyRef)

  playerData = computed<Player | null>(() => {
    return this.playerService.getPlayerData()
  })
  seasonTotals = computed<SeasonTotals[] | null>(() => {
    return this.playerService.getSeasonTotals()
  })
  regSeasonAwards = computed<Award[]>(() => {
    return this.playerData()?.awards.filter((award) => {
      return this.regSeasonAwardNames.includes(award.awardName);
    }) ?? []
  })
  postSeasonAwards = computed<Award[]>(() => {
    return this.playerData()?.awards.filter((award) => {
      return award.awardName === 'Conn Smythe Trophy';
    }) ?? []
  })

  loading = computed<boolean>(() => {
    return this.playerService.playerDataIsLoading() || this.playerService.seasonTotalsIsLoading()
  })

  private regSeasonAwardNames = ['Stanley Cup', 'Vezina Trophy', 'Hart Memorial Trophy', 'Calder Memorial Trophy', 'James Norris Memorial Trophy', 'Frank J. Selke Trophy']

  ngOnInit(): void {
    const subscription = this.activatedRoute.paramMap.subscribe({
      next: (paramMap) => {
        this.playerService.setPlayerID(Number(paramMap.get('playerID')))
      }
    })

    this.destroyRef.onDestroy(() => subscription.unsubscribe())
  }

}
