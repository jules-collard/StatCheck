import { Component, DestroyRef, inject, OnInit } from '@angular/core';

import { PlayerDetails } from "./player-details/player-details";
import { PlayerSeasonTotals } from "./player-season-totals/player-season-totals";
import { PlayerService } from './player.service';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-player-page',
  imports: [PlayerDetails, PlayerSeasonTotals],
  templateUrl: './player-page.html',
  styleUrl: './player-page.css'
})
export class PlayerPage implements OnInit {
  private playerService = inject(PlayerService);
  private activatedRoute = inject(ActivatedRoute);
  private destroyRef = inject(DestroyRef)

  ngOnInit(): void {
    const subscription = this.activatedRoute.paramMap.subscribe({
      next: (paramMap) => {
        this.playerService.setPlayerID(Number(paramMap.get('playerID')))
      }
    })

    this.destroyRef.onDestroy(() => subscription.unsubscribe())
  }
}
