import { Component, computed, inject } from '@angular/core';
import { FormsModule } from '@angular/forms'
import { PlayerService } from '../player-page/player.service';
import { SearchResult } from './search-result.model';
import { Router, RouterLink } from '@angular/router';

@Component({
  selector: 'app-search',
  imports: [FormsModule, RouterLink],
  templateUrl: './search.html',
  styleUrl: './search.css'
})
export class Search {
  private router = inject(Router)
  private playerService = inject(PlayerService);
  enteredPlayerID = '';

  playerList = computed<SearchResult[] | null>(() => {
    return this.playerService.getAllPlayers();
  })

  onFindPlayer() {
    this.router.navigate(['/players', this.enteredPlayerID]);
  }
}
