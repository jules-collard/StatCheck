import { HttpClient } from '@angular/common/http';
import { Component, DestroyRef, inject, input, OnInit, signal } from '@angular/core';

import { Player } from './player.model';
import { PlayerInfo } from './player-info/player-info';
import { PlayerService } from './player.service';

@Component({
  selector: 'app-player-page',
  imports: [PlayerInfo],
  templateUrl: './player-page.html',
  styleUrl: './player-page.css'
})
export class PlayerPage implements OnInit {;
  private destroyRef = inject(DestroyRef);
  private playerService = inject(PlayerService)

  id = input.required<number>();
  playerData = signal<Player | null>(null)
  error = signal('')

  ngOnInit() {
    const subscription = this.playerService.fetchPlayerData(this.id()).subscribe({
      next: (resData) => {
        this.playerData.set(resData);
      },
      error: (error) => {
        console.log(error)
        this.error.set("Error fetching player data.")
      }
    });

    this.destroyRef.onDestroy(() => {
      subscription.unsubscribe();
    });
  }
}
