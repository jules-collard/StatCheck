import { Component, DestroyRef, inject, OnInit, output, signal } from '@angular/core';
import { PlayerService } from '../player-page/player.service';
import { SearchResult } from './search-result.model';

@Component({
  selector: 'app-search',
  imports: [],
  templateUrl: './search.html',
  styleUrl: './search.css'
})
export class Search implements OnInit {
  private destroyRef = inject(DestroyRef);
  private playerService = inject(PlayerService)

  playerList = signal<SearchResult[]>([])
  filteredPlayerList = signal<SearchResult[]>([])
  findPlayer = output<number>()

  ngOnInit() {
    const subscription = this.playerService.fetchAllPlayers().subscribe({
      next: (resData) => {
        this.playerList.set(resData);
      },
      error: (error) => {
        console.log(error)
      }
    });

    this.destroyRef.onDestroy(() => {
      subscription.unsubscribe();
    });
  }

  onFindPlayer() {
    this.findPlayer.emit(8470613)
  }
}
