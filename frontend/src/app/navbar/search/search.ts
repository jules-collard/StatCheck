import { Component, computed, inject, output, signal } from '@angular/core';
import { FormsModule } from '@angular/forms'
import { RouterLink } from '@angular/router';
import { PlayerListService } from '../../player-list/player-list.service';

@Component({
  selector: 'app-search',
  imports: [FormsModule, RouterLink],
  templateUrl: './search.html',
  styleUrl: './search.css'
})
export class Search {
  private playerListService = inject(PlayerListService)
  enteredPlayerName = '';

  onFindPlayer() {
    // this.router.navigate(['/players', this.enteredPlayerID]);
    this.playerListService.setNameToSearch(this.enteredPlayerName)
  }
}
