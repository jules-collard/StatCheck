import { Component, inject, input, output } from '@angular/core';
import { PlayerListService } from '../player-list.service';

@Component({
  selector: 'app-player-list-button',
  imports: [],
  templateUrl: './player-list-button.html',
  styleUrl: './player-list-button.css'
})
export class PlayerListButton {
  listService = inject(PlayerListService);
}
