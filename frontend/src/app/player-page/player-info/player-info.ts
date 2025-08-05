import { Component, computed, DestroyRef, inject, input, signal } from '@angular/core';
import { Player } from '../player.model';
import { MatCardModule } from '@angular/material/card';
import { AgePipe } from '../../pipes/age.pipe';
import { HeightPipe } from '../../pipes/height-pipe';
import { PlayerService } from '../player.service';

@Component({
  selector: 'app-player-info',
  imports: [MatCardModule, AgePipe, HeightPipe],
  templateUrl: './player-info.html',
  styleUrl: './player-info.css'
})
export class PlayerInfo {
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
