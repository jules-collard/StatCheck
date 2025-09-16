import { Component, computed, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Control, form } from '@angular/forms/signals';
import { PlayerListService } from '../player-list/player-list.service';
import { formatCurrency } from '@angular/common';
import { HttpParams } from '@angular/common/http';

@Component({
  selector: 'app-player-filter',
  imports: [FormsModule, Control],
  templateUrl: './player-filter.html',
  styleUrl: './player-filter.css'
})
export class PlayerFilter {
  playerListService = inject(PlayerListService)

  activeRetired = signal<{active: boolean; retired: boolean;}>({
    active: false,
    retired: false
  })

  activeRetiredForm = form(this.activeRetired)

  playersToShow = computed<string>(() => {
    if (this.activeRetiredForm.active().value()) { return 'active' }
    else if (this.activeRetiredForm.retired().value()) { return 'retired' }
    else { return 'all' }
  })

  onChangeActiveRetired() {
    if (!this.activeRetiredForm.active().value() && !this.activeRetiredForm.retired().value()) {
      this.playerListService.filterParams.update(params =>
        ({...params, active: true, retired: true})
      )
    } else {
      this.playerListService.filterParams.update(params =>
        ({...params, active: this.activeRetiredForm.active().value(), retired: this.activeRetiredForm.retired().value()})
      )
    }
  }

  resetActiveRetired() {
    this.activeRetiredForm.active().value.set(false)
    this.activeRetiredForm.retired().value.set(false)
    this.onChangeActiveRetired()
  }
}
