import { Component, computed, inject } from '@angular/core';
import { FormsModule } from '@angular/forms'
import { PlayerService } from '../player-page/player.service';
import { SearchResult } from './search-result.model';

@Component({
  selector: 'app-search',
  imports: [FormsModule],
  templateUrl: './search.html',
  styleUrl: './search.css'
})
export class Search {
  private playerService = inject(PlayerService);
  enteredPlayerID = '';

  playerList = computed<SearchResult[] | null>(() => {
    return this.playerService.getAllPlayers();
  })

  onFindPlayer() {
    this.playerService.setPlayerID(Number(this.enteredPlayerID));
  }
}
