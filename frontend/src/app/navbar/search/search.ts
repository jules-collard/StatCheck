import { Component, inject } from '@angular/core';
import { FormsModule } from '@angular/forms'
import { Router } from '@angular/router';
import { PlayerListService } from '../../search-page/player-list/player-list.service';
import { SearchService } from '../../search-page/search.service';

@Component({
  selector: 'app-search',
  imports: [FormsModule],
  templateUrl: './search.html',
  styleUrl: './search.css'
})
export class Search {
  private playerListService = inject(PlayerListService)
  private searchService = inject(SearchService)
  private router = inject(Router)
  enteredPlayerName = '';

  onFindPlayer() {
    this.playerListService.setNameToSearch(this.enteredPlayerName)
    this.searchService.firstPage()
    this.router.navigate(['search'])
  }
}
