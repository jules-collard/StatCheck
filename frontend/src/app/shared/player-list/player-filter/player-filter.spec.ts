import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PlayerFilter } from './player-filter';

describe('PlayerFilter', () => {
  let component: PlayerFilter;
  let fixture: ComponentFixture<PlayerFilter>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PlayerFilter]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PlayerFilter);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
