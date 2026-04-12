---
layout: page
title: Photography        
permalink: /photography/  
description: Photography — landscape, wildlife, and portraits.
nav: true
nav_order: 5
---

<div class="photography-contact">
  <p>If you would like to purchase any photo or would like to collaborate with me for a photoshoot, please reach out to me at <a href="mailto:utkarsh.srivastava6002@gmail.com">utkarsh.srivastava6002@gmail.com</a>.</p>
</div>

<div class="photography-landing">
  <a href="/photography/landscape/" class="photography-card">
    <div class="photography-card-img-wrapper">
      <img src="/assets/img/photography/landscape/cover.jpg" alt="Landscape Photography" class="photography-card-img">
    </div>
    <div class="photography-card-overlay">
      <h2 class="photography-card-title">Landscape</h2>
      <p class="photography-card-subtitle">Scenic vistas and natural environments</p>
    </div>
  </a>

  <a href="/photography/wildlife/" class="photography-card">
    <div class="photography-card-img-wrapper">
      <img src="/assets/img/photography/wildlife/cover.jpg" alt="Wildlife Photography" class="photography-card-img">
    </div>
    <div class="photography-card-overlay">
      <h2 class="photography-card-title">Wildlife</h2>
      <p class="photography-card-subtitle">Animals in their natural habitat</p>
    </div>
  </a>

  <a href="/photography/portraits/" class="photography-card">
    <div class="photography-card-img-wrapper">
      <img src="/assets/img/photography/portraits/cover.jpg" alt="Portrait Photography" class="photography-card-img">
    </div>
    <div class="photography-card-overlay">
      <h2 class="photography-card-title">Portraits</h2>
      <p class="photography-card-subtitle">People and character studies</p>
    </div>
  </a>
</div>

<style>
.photography-landing {
  display: flex;
  flex-direction: column;
  gap: 2rem;
  margin-top: 1.5rem;
}

.photography-card {
  position: relative;
  display: block;
  width: 100%;
  height: 320px;
  border-radius: 12px;
  overflow: hidden;
  text-decoration: none;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.photography-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.4);
  text-decoration: none;
}

.photography-card-img-wrapper {
  width: 100%;
  height: 100%;
}

.photography-card-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
  filter: brightness(0.65);
}

.photography-card:hover .photography-card-img {
  transform: scale(1.04);
  filter: brightness(0.55);
}

.photography-card-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  padding: 2rem;
  background: linear-gradient(to top, rgba(0,0,0,0.7) 0%, transparent 100%);
}

.photography-card-title {
  color: #ffffff;
  font-size: 2rem;
  font-weight: 700;
  margin: 0;
  letter-spacing: 0.02em;
}

.photography-card-subtitle {
  color: rgba(255,255,255,0.85);
  font-size: 1rem;
  margin: 0.3rem 0 0 0;
}

.photography-contact {
  margin-bottom: 1.5rem;
  text-align: left;
  font-size: 1.05rem;
  color: var(--global-text-color);
}

.photography-contact a {
  color: var(--global-theme-color);
  font-weight: 600;
  text-decoration: none;
}

.photography-contact a:hover {
  text-decoration: underline;
}
</style>
