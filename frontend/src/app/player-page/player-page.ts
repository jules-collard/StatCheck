import { Component, DestroyRef, inject, input, OnInit, signal } from '@angular/core';

import { PlayerDetails } from "./player-details/player-details";
import { PlayerSeasonTotals } from "./player-season-totals/player-season-totals";
import { Player } from './player.model';
import { PlayerService } from './player.service';

@Component({
  selector: 'app-player-page',
  imports: [PlayerDetails, PlayerSeasonTotals],
  templateUrl: './player-page.html',
  styleUrl: './player-page.css'
})
export class PlayerPage implements OnInit {;
  private destroyRef = inject(DestroyRef);
  private playerService = inject(PlayerService)
  
  id = input.required<number>()
  playerData = signal<Player | null>(null)
  error = signal('')

  ngOnInit() {
    const subscription = this.playerService.fetchPlayerData(this.id()).subscribe({
      next: (resData) => {
        this.playerData.set(resData);
      },
      error: (error) => {
        console.log(error)
        this.error.set("Player not found")
      }
    });

    this.destroyRef.onDestroy(() => {
      subscription.unsubscribe();
    });
  }
}
