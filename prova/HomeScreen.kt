@file:OptIn(ExperimentalMaterial3Api::class)

package com.divenire.aereswalls.ui.screens

import androidx.compose.foundation.Image
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Favorite
import androidx.compose.material.icons.filled.Settings
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalLifecycleOwner
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.lifecycle.Lifecycle
import androidx.lifecycle.LifecycleEventObserver
import androidx.navigation.NavController
import coil.compose.rememberAsyncImagePainter
import com.divenire.aereswalls.utils.PreferencesManager

@Composable
fun HomeScreen(navController: NavController) {
    val categories = listOf(
        Category(
            title = "Astrophotography",
            imageUrl = "https://images.unsplash.com/photo-1549887534-1568f8fbd933",
            route = "astro"
        ),
        Category(
            title = "Nature",
            imageUrl = "https://images.unsplash.com/photo-1506744038136-46273834b3fb",
            route = "nature"
        ),
        Category(
            title = "Cityscapes",
            imageUrl = "https://images.unsplash.com/photo-1494526585095-c41746248156",
            route = "city"
        ),
        Category(
            title = "Abstract",
            imageUrl = "https://images.unsplash.com/photo-1520174691701-bc555a3404ca",
            route = "abstract"
        ),
        Category(
            title = "Space",
            imageUrl = "https://images.unsplash.com/photo-1477201227241-8e276f3e1cd1",
            route = "space"
        ),
        Category(
            title = "Minimal",
            imageUrl = "https://images.unsplash.com/photo-1495954484750-af469f2f9be5",
            route = "minimal"
        )
    )

    Scaffold(
        topBar = {
            TopAppBar(
                title = {
                    Box(
                        modifier = Modifier.fillMaxWidth(),
                        contentAlignment = Alignment.Center
                    ) {
                        Text(
                            "Aeres Wallpapers",
                            style = MaterialTheme.typography.titleLarge.copy(fontWeight = FontWeight.Bold)
                        )
                    }
                },
                actions = {
                    IconButton(onClick = { navController.navigate("settings") }) {
                        Icon(Icons.Default.Settings, contentDescription = "Settings")
                    }
                }
            )
        }
    ) { paddingValues ->
        Column(
            modifier = Modifier
                .padding(paddingValues)
                .fillMaxSize()
                .padding(16.dp)
        ) {
            FavoriteSection(navController)
            Spacer(modifier = Modifier.height(24.dp))

            Text(
                "Categorie di sfondi",
                style = MaterialTheme.typography.titleMedium.copy(fontWeight = FontWeight.Bold)
            )
            Spacer(modifier = Modifier.height(16.dp))

            LazyVerticalGrid(
                columns = GridCells.Fixed(3),
                verticalArrangement = Arrangement.spacedBy(12.dp),
                horizontalArrangement = Arrangement.spacedBy(12.dp),
                modifier = Modifier.fillMaxHeight()
            ) {
                items(categories) { category ->
                    CategoryItem(
                        title = category.title,
                        imageUrl = category.imageUrl
                    ) {
                        navController.navigate(category.route)
                    }
                }
            }
        }
    }
}

@Composable
fun FavoriteSection(navController: NavController) {
    val context = LocalContext.current
    val prefs = remember { PreferencesManager(context) }
    var favoriteCount by remember { mutableStateOf(0) }

    val lifecycleOwner = LocalLifecycleOwner.current
    DisposableEffect(lifecycleOwner) {
        val observer = LifecycleEventObserver { _, event ->
            if (event == Lifecycle.Event.ON_RESUME) {
                favoriteCount = prefs.getFavorites().size
            }
        }
        lifecycleOwner.lifecycle.addObserver(observer)
        onDispose {
            lifecycleOwner.lifecycle.removeObserver(observer)
        }
    }

    Card(
        modifier = Modifier
            .fillMaxWidth()
            .clickable { navController.navigate("favorites") },
        elevation = CardDefaults.cardElevation(4.dp)
    ) {
        Row(
            verticalAlignment = Alignment.CenterVertically,
            modifier = Modifier.padding(16.dp)
        ) {
            Icon(
                Icons.Default.Favorite,
                contentDescription = "Favorites",
                tint = Color.Red
            )
            Spacer(modifier = Modifier.width(12.dp))
            Text("Preferiti ($favoriteCount)", style = MaterialTheme.typography.bodyLarge)
        }
    }
}

@Composable
fun CategoryItem(title: String, imageUrl: String, onClick: () -> Unit) {
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .clickable { onClick() },
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Card(
            modifier = Modifier
                .fillMaxWidth()
                .aspectRatio(0.65f),
            elevation = CardDefaults.cardElevation(4.dp),
            shape = MaterialTheme.shapes.medium
        ) {
            Image(
                painter = rememberAsyncImagePainter(imageUrl),
                contentDescription = title,
                contentScale = ContentScale.Crop,
                modifier = Modifier.fillMaxSize()
            )
        }
        Spacer(modifier = Modifier.height(6.dp))
        Text(
            title,
            style = MaterialTheme.typography.bodyMedium.copy(fontWeight = FontWeight.Medium),
            modifier = Modifier.padding(horizontal = 4.dp),
            maxLines = 1
        )
    }
}

data class Category(
    val title: String,
    val imageUrl: String,
    val route: String
)
