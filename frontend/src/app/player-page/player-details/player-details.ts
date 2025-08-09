import { Component, DestroyRef, inject, input, signal, OnInit } from '@angular/core';
import { PlayerService } from '../player.service';
import { Player } from '../player.model';
import { AgePipe } from '../../pipes/age.pipe';
import { HeightPipe } from '../../pipes/height-pipe';

@Component({
  selector: 'app-player-details',
  imports: [AgePipe, HeightPipe],
  templateUrl: './player-details.html',
  styleUrl: './player-details.css'
})
export class PlayerDetails implements OnInit {
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
