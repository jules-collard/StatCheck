import { HttpClient } from '@angular/common/http';
import { Component, DestroyRef, inject, input, signal } from '@angular/core';

import { Player } from './player.model';

@Component({
  selector: 'app-player-page',
  imports: [],
  templateUrl: './player-page.html',
  styleUrl: './player-page.css'
})
export class PlayerPage {
  private httpClient = inject(HttpClient);
  private destroyRef = inject(DestroyRef);

  id = input.required<number>()
  playerData = signal<Player | undefined>(undefined)

  ngOnInit() {
    const subscription = this.httpClient.get<Player>('http://localhost:5000/api/players/'+ this.id).subscribe({
      next: (resData) => {
        this.playerData.set(resData)
      }
    });

    this.destroyRef.onDestroy(() => {
      subscription.unsubscribe()
    });
  }
}
